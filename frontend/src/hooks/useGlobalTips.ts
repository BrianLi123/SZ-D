import { App } from 'antd';
import type { MessageInstance } from 'antd/es/message/interface';
import type { ModalStaticFunctions } from 'antd/es/modal/confirm';
import type { NotificationInstance } from 'antd/es/notification/interface';

const message = {} as MessageInstance;
const notification = {} as NotificationInstance;
const modal = {} as Omit<ModalStaticFunctions, 'warn'>;

export default function useGlobalTips() {
  const staticFunction = App.useApp();
  Object.assign(message, staticFunction.message);
  Object.assign(modal, staticFunction.modal);
  Object.assign(notification, staticFunction.notification);
  return null;
}

export { message, notification, modal };
