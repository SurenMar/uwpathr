'use client';

import { useState, useEffect } from 'react';

interface CoursePathNode {
  id: string;
  node_type: string;
  target_course?: {
    id: string;
    code: string;
    number: string;
    title: string;
  };
  leaf_course?: {
    id: string;
    code: string;
    number: string;
    title: string;
  };
  num_children_required?: number;
  children: CoursePathNode[];
}

interface SelectedPathNode {
  prerequisite_node: string;
  target_course: number;
  children: SelectedPathNode[];
}

interface CoursePathModalProps {
  isOpen: boolean;
  onClose: () => void;
  courseId: number;
  courseName: string;
}

export default function CoursePathModal({
  isOpen,
  onClose,
  courseId,
  courseName,
}: CoursePathModalProps) {
  const [rootNode, setRootNode] = useState<CoursePathNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedNodeIds, setExpandedNodeIds] = useState<Set<string>>(new Set());
  const [selectedNodeIds, setSelectedNodeIds] = useState<Set<string>>(new Set());
  const [selectedPathTree, setSelectedPathTree] = useState<SelectedPathNode | null>(null);

  // Reset state when modal closes or courseId changes
  useEffect(() => {
    if (!isOpen) {
      setRootNode(null);
      setLoading(false);
      setError(null);
      setExpandedNodeIds(new Set());
      setSelectedNodeIds(new Set());
      setSelectedPathTree(null);
    }
  }, [isOpen, courseId]);

  // Fetch prerequisite tree when modal opens
  useEffect(() => {
    if (!isOpen || !courseId) return;

    const fetchPrerequisiteTree = async () => {
      setLoading(true);
      setError(null);
      try {
        const url = `${process.env.NEXT_PUBLIC_HOST}/api/prerequisites/?target_course=${courseId}`;
        const response = await fetch(url, {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch prerequisite tree');
        }
        const data = await response.json();
        
        console.log('Full API response:', data);
        
        // The API returns an array directly (not paginated)
        if (Array.isArray(data) && data.length > 0) {
          console.log('Root node:', data[0]);
          setRootNode(data[0]);
          // Expand all nodes by default to show full tree
          const getAllNodeIds = (node: CoursePathNode): string[] => {
            const ids = [node.id];
            if (node.children) {
              node.children.forEach(child => {
                ids.push(...getAllNodeIds(child));
              });
            }
            return ids;
          };
          setExpandedNodeIds(new Set(getAllNodeIds(data[0])));
          
          // Initialize root node as selected
          setSelectedNodeIds(new Set([data[0].id]));
          setSelectedPathTree({
            prerequisite_node: data[0].id,
            target_course: courseId,
            children: []
          });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPrerequisiteTree();
  }, [isOpen, courseId]);

  const toggleNodeExpanded = (nodeId: string) => {
    setExpandedNodeIds(prev => {
      const newSet = new Set(prev);
      if (newSet.has(nodeId)) {
        newSet.delete(nodeId);
      } else {
        newSet.add(nodeId);
      }
      return newSet;
    });
  };

  // Helper to find a node in the tree by ID
  const findNodeById = (node: CoursePathNode, targetId: string): CoursePathNode | null => {
    if (node.id === targetId) return node;
    if (node.children) {
      for (const child of node.children) {
        const found = findNodeById(child, targetId);
        if (found) return found;
      }
    }
    return null;
  };

  // Helper to find parent of a node
  const findParentNode = (node: CoursePathNode, targetId: string): CoursePathNode | null => {
    if (node.children) {
      for (const child of node.children) {
        if (child.id === targetId) return node;
        const found = findParentNode(child, targetId);
        if (found) return found;
      }
    }
    return null;
  };

  // Helper to get all descendant IDs of a node
  const getAllDescendantIds = (node: CoursePathNode): string[] => {
    const ids: string[] = [];
    if (node.children) {
      node.children.forEach(child => {
        ids.push(child.id);
        ids.push(...getAllDescendantIds(child));
      });
    }
    return ids;
  };

  // Helper to count selected children of a node
  const countSelectedChildren = (node: CoursePathNode): number => {
    if (!node.children) return 0;
    return node.children.filter(child => selectedNodeIds.has(child.id)).length;
  };

  // Helper to check if a node can be selected
  const canSelectNode = (nodeId: string): boolean => {
    if (!rootNode) return false;
    
    // Root is always selectable (to deselect)
    if (nodeId === rootNode.id) return true;
    
    // Find the node and its parent
    const node = findNodeById(rootNode, nodeId);
    const parent = findParentNode(rootNode, nodeId);
    
    if (!node || !parent) return false;
    
    // Parent must be selected
    if (!selectedNodeIds.has(parent.id)) return false;
    
    // If node is already selected, it can be deselected
    if (selectedNodeIds.has(nodeId)) return true;
    
    // Check if parent has room for more children
    const selectedCount = countSelectedChildren(parent);
    const required = parent.num_children_required ?? 0;
    
    return selectedCount < required;
  };

  // Helper to remove a node from the selected path tree
  const removeNodeFromPathTree = (tree: SelectedPathNode, nodeId: string): SelectedPathNode | null => {
    // If this is the node to remove, return null
    if (tree.prerequisite_node === nodeId) return null;
    
    // Filter out children that match the nodeId
    const newChildren = tree.children
      .map(child => removeNodeFromPathTree(child, nodeId))
      .filter((child): child is SelectedPathNode => child !== null);
    
    return {
      ...tree,
      children: newChildren
    };
  };

  // Helper to add a node to the selected path tree
  const addNodeToPathTree = (tree: SelectedPathNode, parentId: string, nodeId: string): SelectedPathNode => {
    if (tree.prerequisite_node === parentId) {
      return {
        ...tree,
        children: [
          ...tree.children,
          {
            prerequisite_node: nodeId,
            target_course: courseId,
            children: []
          }
        ]
      };
    }
    
    return {
      ...tree,
      children: tree.children.map(child => addNodeToPathTree(child, parentId, nodeId))
    };
  };

  // Handle node selection/deselection
  const toggleNodeSelection = (nodeId: string) => {
    if (!rootNode || !canSelectNode(nodeId)) return;
    
    const isSelected = selectedNodeIds.has(nodeId);
    
    if (isSelected) {
      // Deselect this node and all its descendants
      const node = findNodeById(rootNode, nodeId);
      if (node) {
        const descendantIds = getAllDescendantIds(node);
        const newSelectedIds = new Set(selectedNodeIds);
        newSelectedIds.delete(nodeId);
        descendantIds.forEach(id => newSelectedIds.delete(id));
        setSelectedNodeIds(newSelectedIds);
        
        // Remove from path tree
        if (selectedPathTree) {
          const newTree = removeNodeFromPathTree(selectedPathTree, nodeId);
          setSelectedPathTree(newTree);
          console.log('Updated path tree (after removal):', JSON.stringify(newTree, null, 2));
        }
      }
    } else {
      // Select this node
      const newSelectedIds = new Set(selectedNodeIds);
      newSelectedIds.add(nodeId);
      setSelectedNodeIds(newSelectedIds);
      
      // Add to path tree
      if (selectedPathTree) {
        const parent = findParentNode(rootNode, nodeId);
        if (parent) {
          const newTree = addNodeToPathTree(selectedPathTree, parent.id, nodeId);
          setSelectedPathTree(newTree);
          console.log('Updated path tree (after addition):', JSON.stringify(newTree, null, 2));
        }
      }
    }
  };

  const renderNode = (node: CoursePathNode, depth = 0, isLast = false, parentPrefix = ''): JSX.Element => {
    const isExpanded = expandedNodeIds.has(node.id);
    const hasChildren = node.children && node.children.length > 0;
    const isSelected = selectedNodeIds.has(node.id);
    const isSelectable = canSelectNode(node.id);
    
    // Tree line characters
    const connector = isLast ? '└── ' : '├── ';
    const childPrefix = parentPrefix + (isLast ? '    ' : '│   ');

    // Determine styling based on selection state
    const opacityClass = isSelected ? 'opacity-100' : 'opacity-60';
    const hoverClass = isSelectable ? 'hover:opacity-100 hover:bg-gray-200' : '';
    const cursorClass = isSelectable ? 'cursor-pointer' : 'cursor-not-allowed';
    const disabledClass = !isSelectable && !isSelected ? 'opacity-30' : '';
    
    // Color classes for selected vs unselected
    const branchColor = isSelected ? 'text-blue-600 font-bold' : 'text-gray-700 hover:text-gray-900';
    const courseColor = isSelected ? 'text-blue-600' : 'text-gray-800 hover:text-gray-950';
    const groupColor = isSelected ? 'text-blue-600' : 'text-blue-800 hover:text-blue-950';

    const handleClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      toggleNodeSelection(node.id);
    };

    const handleExpandClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      if (hasChildren) {
        toggleNodeExpanded(node.id);
      }
    };

    return (
      <div key={node.id}>
        <div 
          className={`flex items-center gap-2 py-1 font-mono text-sm transition-opacity ${opacityClass} ${hoverClass} ${cursorClass} ${disabledClass}`}
          onClick={handleClick}
        >
          <span className={branchColor}>{parentPrefix}{connector}</span>
          
          {node.node_type === 'course' && node.leaf_course ? (
            <span className={`font-medium ${courseColor}`}>
              {node.leaf_course.code} {node.leaf_course.number}
            </span>
          ) : (
            <span className={`font-medium ${groupColor}`}>
              {node.num_children_required === 1 
                ? `One of` 
                : node.num_children_required === node.children?.length
                ? `All of`
                : `${node.num_children_required} of ${node.children?.length}`}
              {hasChildren && (
                <span 
                  className={branchColor}
                  onClick={handleExpandClick}
                >
                  {isExpanded ? '▼' : '▶'}
                </span>
              )}
            </span>
          )}
        </div>

        {isExpanded && hasChildren && (
          <div>
            {node.children?.map((child, index) => 
              renderNode(child, depth + 1, index === node.children!.length - 1, childPrefix)
            )}
          </div>
        )}
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">
            Prerequisites for {courseName}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          {loading && (
            <div className="flex items-center justify-center h-32">
              <svg className="w-8 h-8 animate-spin text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" opacity="0.25" />
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700">
              Error: {error}
            </div>
          )}

          {rootNode && !loading && (
            <div className="flex flex-col items-center py-6 relative">
              {/* Root course at top */}
              <div className="font-bold text-xl text-gray-900 mb-2 relative z-10">
                {rootNode.target_course?.code} {rootNode.target_course?.number}
              </div>
              
              {/* Root requirement description */}
              {rootNode.children && rootNode.children.length > 0 && (
                <div className="text-sm font-semibold text-purple-600 mb-4">
                  {rootNode.num_children_required === 1 
                    ? 'One of' 
                    : rootNode.num_children_required === rootNode.children?.length
                    ? 'All of'
                    : `${rootNode.num_children_required} of ${rootNode.children?.length}`}
                </div>
              )}
              
              {/* Prerequisites tree */}
              {rootNode.children && rootNode.children.length > 0 && (
                <div className="flex items-start gap-12 relative">
                  {/* SVG for connecting lines from root */}
                  <svg 
                    className="absolute left-0 top-0 w-full h-full pointer-events-none" 
                    style={{ overflow: 'visible' }}
                  >
                    {/* Vertical line from root to horizontal connector */}
                    <line 
                      x1="50%" 
                      y1="-16" 
                      x2="50%" 
                      y2="20" 
                      stroke="#9CA3AF" 
                      strokeWidth="2"
                    />
                    
                    {rootNode.children.length > 1 ? (
                      <>
                        {/* Horizontal line */}
                        <line 
                          x1={`${50 / rootNode.children.length}%`}
                          y1="20" 
                          x2={`${100 - (50 / rootNode.children.length)}%`}
                          y2="20" 
                          stroke="#9CA3AF" 
                          strokeWidth="2"
                        />
                        {/* Vertical lines to each child */}
                        {rootNode.children.map((_, index) => {
                          const xPos = ((index + 0.5) / rootNode.children!.length) * 100;
                          return (
                            <line 
                              key={index}
                              x1={`${xPos}%`}
                              y1="20" 
                              x2={`${xPos}%`}
                              y2="40" 
                              stroke="#9CA3AF" 
                              strokeWidth="2"
                            />
                          );
                        })}
                      </>
                    ) : (
                      /* Single child - just straight line */
                      <line 
                        x1="50%" 
                        y1="20" 
                        x2="50%" 
                        y2="40" 
                        stroke="#9CA3AF" 
                        strokeWidth="2"
                      />
                    )}
                  </svg>
                  
                  {rootNode.children.map((child) => (
                    <div key={child.id} className="pt-8">
                      {renderNode(child)}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 font-medium rounded-lg hover:bg-gray-100 transition-colors"
          >
            Close
          </button>
          <button
            className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Save Path
          </button>
        </div>
      </div>
    </div>
  );
}
