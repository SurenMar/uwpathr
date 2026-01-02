"use client";

import { useState } from "react";

export default function SidebarResourcesDropdown() {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setOpen(!open)}>
        Resources
      </button>

      {open && (
        <div className="dropdown">
          <a 
            href="https://cs.uwaterloo.ca"
            target="_blank"
            rel="noopener noreferrer"
              >UW CS Home Page
          </a>
          <a 
            href="https://uwaterloo.ca/computer-science/advising"
            target="_blank"
            rel="noopener noreferrer"
              >UW CS Advising
          </a>
        </div>
      )}
    </div>
  );
}
