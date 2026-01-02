import { ImSpinner } from "react-icons/im";
import cn from "classnames";

interface Props {
  sm?: boolean;
  md?: boolean;
  lg?: boolean;
}

export default function Spinner({ sm, md, lg }: Props ) {
  const className = cn('animate-spin text-white-300 fill-white-300 mr-2', {
    'w-4 h-4': sm,
    'w-6 h-6': md,
    'w-8 h-8': lg,
  });

  return (
    <div className="flex items-center justify-center">
      <div 
        className="w-8 h-8 border-4 border-blue-500 border-dashed rounded-full animate-spin"
        role='status'
      >
        <ImSpinner className="w-full h-full text-blue-500" />
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
}