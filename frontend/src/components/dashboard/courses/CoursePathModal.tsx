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

  const renderNode = (node: CoursePathNode, level: number = 0): JSX.Element => {
    const isExpanded = expandedNodeIds.has(node.id);
    const hasChildren = node.children && node.children.length > 0;
    const isLeaf = node.node_type === 'course';
    const isRoot = level === 0;

    // For root node, show target course
    const displayCourse = isRoot ? node.target_course : node.leaf_course;

    return (
      <div key={node.id} style={{ marginLeft: `${level * 24}px` }}>
        <div className="flex items-center gap-2 py-2 px-3 hover:bg-gray-100 rounded cursor-pointer"
             onClick={() => hasChildren && toggleNodeExpanded(node.id)}>
          {hasChildren ? (
            <svg
              className={`w-4 h-4 transition-transform ${
                isExpanded ? 'rotate-90' : ''
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          ) : (
            <div className="w-4" />
          )}

          {isLeaf || isRoot ? (
            <div className="flex-1">
              <div className="font-medium text-gray-900">
                {displayCourse?.code} {displayCourse?.number}
              </div>
              <div className="text-sm text-gray-600">
                {displayCourse?.title}
              </div>
            </div>
          ) : (
            <div className="flex-1">
              <div className="font-medium text-blue-600">
                {node.num_children_required ? `${node.num_children_required} of ${node.children.length} required` : 'All required'}
              </div>
            </div>
          )}
        </div>

        {hasChildren && isExpanded && (
          <div>
            {node.children.map(child => renderNode(child, level + 1))}
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
            <div className="space-y-1">
              <div>Root node exists: {rootNode.id}</div>
              <div>Node type: {rootNode.node_type}</div>
              <div>Has children: {rootNode.children?.length || 0}</div>
              {renderNode(rootNode)}
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
