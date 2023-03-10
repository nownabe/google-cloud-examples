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

const searchDocuments = async (
  content: string
): Promise<ApiResult<Array<Document>>> => {
  try {
    const response = await DefaultService.searchDocumentsDocumentsSearchGet(
      content
    );
    return {
      ok: true,
      data: response.documents,
    };
  } catch (e) {
    return handleErrorResponse(e);
  }
};

const createFeedback = async (
  content: string,
  documentId: string,
  score: number
): Promise<ApiResult<null>> => {
  try {
    await DefaultService.createFeedbackFeedbacksPost({
      content,
      document_id: documentId,
      score,
    });
    return { ok: true, data: null };
  } catch (e) {
    console.error(e);
    return handleErrorResponse(e);
  }
};

export { createDocument, searchDocuments, createFeedback };
