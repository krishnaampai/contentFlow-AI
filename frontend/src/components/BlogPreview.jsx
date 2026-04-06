// import ReactMarkdown from "react-markdown"

// export default function BlogPreview({ content, view }) {
//   if (view === "mobile") {
//     return (
//       <div className=" flex justify-center">
//       <div className="w-93.75 h-162.5 bg-black rounded-[2.5rem] p-2 shadow-2xl scale-75 origin-top">
//         <div className="w-full h-full bg-white rounded-4xl overflow-hidden flex flex-col">
//           <div className="h-6 flex justify-center items-center text-xs text-gray-500">9:41</div>
//           <div className="px-4 py-2 border-b text-sm font-medium">Blog</div>
//           <div className="flex-1 overflow-y-auto p-4">
//             <div className="prose prose-sm max-w-none text-[#3b2f2f]">
//               <ReactMarkdown>{content}</ReactMarkdown>
//             </div>
//           </div>
//           <div className="h-10 border-t flex justify-center items-center text-gray-400">⬤</div>
//         </div>
//       </div>
//       </div>
//     )
//   }

//   return (
//     <div className="w-full max-w-4xl bg-gray-200 rounded-xl shadow-inner p-4">
//       <div className="flex items-center gap-2 mb-3">
//         <div className="w-3 h-3 bg-red-400 rounded-full"></div>
//         <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
//         <div className="w-3 h-3 bg-green-400 rounded-full"></div>
//         <div className="ml-3 text-xs text-gray-500 bg-white px-3 py-1 rounded-md">
//           contentflow.ai/blog
//         </div>
//       </div>
//       <div className="bg-white rounded-lg shadow p-6">
//         <div className="prose max-w-full text-[#3b2f2f]">
//           <ReactMarkdown>{content}</ReactMarkdown>
//         </div>
//       </div>
//     </div>
//   )
// }

// import ReactMarkdown from "react-markdown"

// export default function BlogPreview({ content, view }) {
//   return (
//     <div className={`bg-white rounded-xl shadow border p-6 ${
//       view === "mobile" ? "max-w-sm mx-auto" : "max-w-4xl mx-auto"
//     }`}>
//       <div className="border-b pb-2 mb-4 text-sm text-gray-500">
//         contentflow.ai/blog
//       </div>
//       <div className="prose prose-sm max-w-none text-[#3b2f2f]">
//         <ReactMarkdown>{content}</ReactMarkdown>
//       </div>
//     </div>
//   )
// }

import ReactMarkdown from "react-markdown"

export default function BlogPreview({ content, view }) {
const cleanedContent = content.replace(/^##\s*BLOG POST.*\n?/i, "")
  return (
    <div
      className={`bg-white rounded-xl shadow border p-4 
      transition-all duration-500 ease-in-out transform
      ${
        view === "mobile"
          ? "h-[70vh] overflow-y-auto max-w-93.75 mx-auto scale-[0.95]"
          : "h-auto scale-100"
      }`}
    >
      <div className="border-b pb-2 mb-3 text-sm text-gray-500">
        BlogPost.com
      </div>

      <ReactMarkdown>{cleanedContent}</ReactMarkdown>
    </div>
  )
}