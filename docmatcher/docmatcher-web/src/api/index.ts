import { ApiError, Document } from "./client";
import { DefaultService } from "./client/services/DefaultService";

const prefix = "/api/v1";

type ApiResultSuccess<T> = { ok: true; data: T };
type ApiResultError = { ok: false; error: { status: number; detail: string } };

type ApiResult<T> = ApiResultSuccess<T> | ApiResultError;

const handleErrorResponse = (e: any): ApiResultError => {
  if (e instanceof ApiError) {
    return {
      ok: false,
      error: {
        status: e.status,
        detail: e.body.detail,
      },
    };
  } else {
    return {
      ok: false,
      error: {
        status: -1,
        detail: "unexpected error",
      },
    };
  }
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
    return handleErrorResponse(e);
  }
};
