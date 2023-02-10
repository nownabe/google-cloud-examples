import { ApiError, Document } from "./client";
import { DefaultService } from "./client/services/DefaultService";

const prefix = "/api/v1";

type ApiResult<T> =
  | {
      ok: true;
      data: T;
    }
  | {
      ok: false;
      error: {
        status: number;
        detail: string;
      };
    };

const createDocument = async (
  content: string
): Promise<ApiResult<Document>> => {
  try {
    const document = await DefaultService.createDocumentDocumentsPost({
      content,
    });
    return {
      ok: true,
      data: document,
    };
  } catch (e) {
    if (e instanceof ApiError) {
      return {
        ok: false,
        error: {
          status: e.status,
          detail: e.body.detail,
        },
      };
    } else {
      console.error(e);
      return {
        ok: false,
        error: {
          status: -1,
          detail: "unexpected error",
        },
      };
    }
  }
};

export { createDocument };
