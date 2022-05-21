import { SiteKey, WidgetConfig, ConfigurationError } from "@mcaptcha/core-glue";
import Receiver from "@mcaptcha/core-glue";
export declare const INPUT_NAME = "mcaptcha__token";
export declare const ID = "mcaptcha__widget-container";
export default class Widget {
    inputElement: HTMLInputElement;
    receiver: Receiver;
    constructor(config: WidgetConfig);
    setToken: (val: string) => string;
}
export { SiteKey, WidgetConfig, ConfigurationError };
