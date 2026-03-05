declare global {
    namespace App {
        interface Platform {
            cf: CfProperties;
            ctx: ExecutionContext;
            env: Env;
        }

        // interface Error {}
        // interface Locals {}
        // interface PageData {}
    }
}

declare module "svelte-m3c" {
    export type IconName = string;
}

export {};
