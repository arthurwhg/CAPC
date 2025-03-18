export default function handler(req, res) {
    //res.status(200).json({ message: "Hello, Next.js API!" });
    if (req.method === "GET") {
        res.status(200).json({ 'methdo': req.method, user: "Got John Doe" });
      } else if (req.method === "POST") {
        const { name } = req.body;
        res.status(201).json({ 'methdo': req.method,message: `Post: User ${name} created!` });
      } else {
        res.status(405).json({ 'methdo': req.method,error: "Method not allowed" });
      }
  }