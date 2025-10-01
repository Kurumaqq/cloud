import axios from "axios";

token =
  "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrdXJ1bWFxcSJ9.l1zrPmhh1eS3b6unBB1wQ2-V_CKSa7d3uDM9z3yYJoeqZQ_1DBzyPK8ztoYRbsWO85vuHiryud5o68j_gQ1v-HRdw6yWcMQwNt5zCYbtOUO_snBbLgKCfywPhcEL_x6mlfO-dfMQNG6u_hL8oVmksGLwWGL02blLGQ3veOFGneHn5UW3529Je3PwakIUeT7eXg2eDPJOzXdohFMdhA52xhXzTz6ZMKM-LFQFyI0g4Kr5lAoHMfWRO3v1hOpAcpUpeEgCEx0o25YTpEE3NCzR7eKvf6XOBhyGFvg154lGpLN9qMvRa8Rx44fJ9vG86WZ7jVyjlUOkV1K0lYbBHaS5sg";

async () => {
  const response = await axios.get("http://127.0.0.1:8001/files/get/test.png", {
    headers: {
      Authorization: token,
    },
  });
  console.log(response);
};
