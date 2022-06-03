/*
 * Copyright (C) 2022  Aravinth Manivannan <realaravinth@batsense.net>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

use crate::AppCtx;

pub const ROUTES: routes::Routes = routes::Routes::new();
const INDEX: &str = include_str!("./static/index.html");
const INDEX_JS: &str = include_str!("./static/index.js");
const PROTECTED: &str = include_str!("./static/protected.html");
const UNPROTECTED: &str = include_str!("./static/unprotected.html");

pub mod routes {

    pub struct Routes {
        pub protected: &'static str,
        pub unprotected: &'static str,
        pub index: &'static str,
        pub index_js: &'static str,
    }

    impl Routes {
        pub const fn new() -> Self {
            let index = "/";
            let index_js = "/index.js";
            let protected = "/protected";
            let unprotected = "/unprotected";
            Routes {
                index,
                protected,
                unprotected,
                index_js,
            }
        }
    }
}

pub mod runners {

    use super::*;

    #[derive(Clone, Debug, Default, PartialEq, Deserialize, Serialize)]
    pub struct Register {
        pub username: String,
        pub password: String,
        pub confirm_password: String,
    }

    #[derive(Clone, Debug, Deserialize, Serialize)]
    pub struct Login {
        // login accepts both username and email under "username field"
        // TODO update all instances where login is used
        pub login: String,
        pub password: String,
    }

    #[derive(Clone, Debug, Deserialize, Serialize)]
    pub struct Password {
        pub password: String,
    }

    pub async fn register_runner(payload: &Register, ctx: &AppCtx) -> Result<(), &'static str> {
        if payload.password != payload.confirm_password {
            return Err("Passowrds don't match");
        }
        let username = ctx.creds.username(&payload.username).unwrap();
        let hash = ctx.creds.password(&payload.password).unwrap();

        sqlx::query!(
            "INSERT INTO users (name , password) values ($1, $2)",
            &username,
            &hash,
        )
        .execute(&ctx.db)
        .await
        .unwrap();
        Ok(())
    }
}

pub fn services(cfg: &mut web::ServiceConfig) {
    cfg.service(protected);
    cfg.service(unprotected);
    cfg.service(unprotected_page);
    cfg.service(protected_page);
    cfg.service(index_js);
    cfg.service(index);
}

#[actix_web_codegen_const_routes::get(path = "ROUTES.index_js")]
async fn index_js() -> impl Responder {
    HttpResponse::Ok()
        .content_type("application/javascript")
        .body(INDEX_JS)
}

#[actix_web_codegen_const_routes::get(path = "ROUTES.protected")]
async fn protected_page(ctx: AppCtx) -> impl Responder {
    let html = actix_web::http::header::ContentType::html();
    let page = PROTECTED.replace("MCAPTCHA_URL_REPLACEME", &ctx.captcha_path);

    HttpResponse::Ok().content_type(html).body(page)
}

#[actix_web_codegen_const_routes::get(path = "ROUTES.unprotected")]
async fn unprotected_page() -> impl Responder {
    let html = actix_web::http::header::ContentType::html();
    HttpResponse::Ok().content_type(html).body(UNPROTECTED)
}

#[actix_web_codegen_const_routes::get(path = "ROUTES.index")]
async fn index() -> impl Responder {
    let html = actix_web::http::header::ContentType::html();
    HttpResponse::Ok().content_type(html).body(INDEX)
}

#[derive(Clone, Debug, Default, PartialEq, Deserialize, Serialize)]
pub struct RegisterProtected {
    pub username: String,
    pub password: String,
    pub confirm_password: String,
    pub mcaptcha__token: String,
}

impl From<RegisterProtected> for runners::Register {
    fn from(r: RegisterProtected) -> Self {
        Self {
            username: r.username,
            password: r.password,
            confirm_password: r.confirm_password,
        }
    }
}

#[actix_web_codegen_const_routes::post(path = "ROUTES.protected")]
async fn protected(payload: web::Form<RegisterProtected>, ctx: AppCtx) -> impl Responder {
    let payload = payload.into_inner();
    if !ctx.verify_token(&payload.mcaptcha__token).await {
        println!("Invalid Captcha");
        HttpResponse::BadRequest().body("Invalid Captcha")
    } else {
        if let Err(e) = runners::register_runner(&payload.into(), &ctx).await {
            HttpResponse::BadRequest().body(e)
        } else {
            HttpResponse::Ok().body("OK").into()
        }
    }
}

#[actix_web_codegen_const_routes::post(path = "ROUTES.unprotected")]
async fn unprotected(payload: web::Form<runners::Register>, ctx: AppCtx) -> impl Responder {
    runners::register_runner(&payload, &ctx).await.unwrap();
    if let Err(e) = runners::register_runner(&payload, &ctx).await {
        HttpResponse::BadRequest().body(e)
    } else {
        HttpResponse::Ok().body("OK").into()
    }
}
