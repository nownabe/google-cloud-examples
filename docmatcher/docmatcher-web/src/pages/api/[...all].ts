// For local development

import { NextApiRequest, NextApiResponse } from "next";
import httpProxyMiddleware from "next-http-proxy-middleware";

export const config = {
  api: {
    externalResolver: true,
    bodyParser: false,
  },
};

export default function proxy(req: NextApiRequest, res: NextApiResponse) {
  if (process.env.NODE_ENV === "development") {
    httpProxyMiddleware(req, res, {
      changeOrigin: true,
      target: "http://127.0.0.1:3001",
    });
  } else {
    res.status(404).send(null);
  }
}
