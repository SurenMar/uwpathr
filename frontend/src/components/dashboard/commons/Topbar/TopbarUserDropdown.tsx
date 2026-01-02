"use client";

import { useState } from "react";

export default function TopbarUserDropdown() {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setOpen(!open)}>
        Me
      </button>

      {open && (
        <div className="dropdown">
          <p>Logout</p>
          <p>Delete Account</p>
        </div>
      )}
    </div>
  );
}
