'use client';

import { ReactNode, useEffect } from "react";
import { useAppDispatch } from "@/store/hooks";
import { setPageTitle } from "@/store/features/topbar/pageTitleSlice";

export default function ChecklistLayout({
  children,
}: {
  children: ReactNode;
}) {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(setPageTitle("Checklist"));
  }, [dispatch]);

  return children;
}
