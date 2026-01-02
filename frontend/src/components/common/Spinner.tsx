import { ImSpinner } from "react-icons/im";
import cn from "classnames";

export default function Spinner({ sm, md, lg }) {
  const classNames = cn(
    "flex",
    "items-center",
    "justify-center",
  );

  return (
    <div className="flex items-center justify-center">
      <div 
        className="w-8 h-8 border-4 border-blue-500 border-dashed rounded-full animate-spin"
        role='status'
      >
        <ImSpinner className="w-full h-full text-blue-500" />
      </div>
    </div>
  );
}