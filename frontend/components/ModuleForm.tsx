// import { useState } from "react";
// import axios from "axios";
// import { useRouter } from "next/router";

// export default function CreateModulePage() {
//   const [moduleCode, setmoduleCode] = useState("");
//   const [message, setMessage] = useState("");
//   const router = useRouter();

//   const handleCreate = async (e: React.FormEvent) => {
//     e.preventDefault();

//     try {
//       const token = localStorage.getItem("token");
//       const response = await axios.post(
//         "http://localhost:8000/api/module/create",
//         { module_code: moduleCode },
//         {
//           headers: {
//             Authorization: `Bearer ${token}`,
//           },
//         }
//       );

//       setMessage(`Module '${response.data.module_code}' created successfully`);
//       setmoduleCode("");
//     } catch (err: any) {
//       setMessage("Failed to create module: " + err.response?.data?.detail);
//     }
//   };

//   return (
//     <div style={{ maxWidth: 400, margin: "40px auto" }}>
//       <h2>Create a New Domain Module</h2>
//       <form onSubmit={handleCreate}>
//         <input
//           type="text"
//           placeholder="Enter module/domain name"
//           value={moduleCode}
//           onChange={(e) => setmoduleCode(e.target.value)}
//           required
//           style={{
//             width: "100%",
//             padding: "10px",
//             marginBottom: "10px",
//           }}
//         />
//         <button type="submit" style={{ padding: "10px 20px" }}>
//           Create
//         </button>
//       </form>
//       {message && <p>{message}</p>}
//     </div>
//   );
// }
