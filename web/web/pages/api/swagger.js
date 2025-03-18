export default function handler(req, res) {
    const swaggerSpec = {
      openapi: "3.0.0",
      info: {
        title: "Next.js API",
        version: "1.0.0",
        description: "API documentation for Next.js",
      },
      paths: {
        "/api/hello": {
          get: {
            summary: "Returns a hello message",
            responses: {
              "200": {
                description: "Success",
                content: {
                  "application/json": {
                    schema: {
                      type: "object",
                      properties: {
                        message: { type: "string" },
                      },
                    },
                  },
                },
              },
            },
          },
        },
      },
    };
  
    res.status(200).json(swaggerSpec);
  }