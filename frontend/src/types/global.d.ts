declare interface LabelValue {
  label: string;
  value: string;
}

declare interface SearchCommonParams {
  pageNum: number;
  pageSize: number;
  sortField?: string;
  sortOrder?: 'descend' | 'ascend' | null;
}

declare interface SuccessResponse<ResDataType = any> {
  logoBase64: string | undefined;
  status: {
    msg: string;
    code: number;
  };
  payload: {
    data: ResDataType;
    total?: number;
    unReadNum?: number;
  };
}

declare module 'papaparse';
