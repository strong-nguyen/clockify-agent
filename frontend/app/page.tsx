import Image from "next/image";
import MainUI from "@/components/MainUI";

export default function Home() {
  return (
    <div className="flex flex-col mt-10">
      <h1 className="text-3xl font-bold mb-10 text-center">Clockify Agent</h1>
      <MainUI />
    </div>
  );
}
