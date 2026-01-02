"use client";

import { ReactNode, useEffect } from "react";
import { useAppDispatch } from "@/store/hooks";
import { setPageTitle } from "@/store/pageTitleSlice";

export default function CoursesLayout({
  children,
}: {
  children: ReactNode;
}) {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(setPageTitle("My Courses"));
  }, [dispatch]);

  return children;
}
