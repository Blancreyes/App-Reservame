import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Inicio } from "./pages/inicio";
import { Demo } from "./pages/demo";
import { Alta_usuario } from "./pages/alta_usuario";
import { Single } from "./pages/single";
import { Password } from "./pages/password";
import { Acceso } from "./pages/acceso";
import { Perfil_Usuario } from "./pages/perfil_usuario";
import { Mis_reservas } from "./pages/mis_reservas";
import injectContext from "./store/appContext";

import { Navbar } from "./component/navbar.jsx";
import { Footer } from "./component/footer";

//create your first component
const Layout = () => {
  //the basename is used when your project is published in a subdirectory and not in the root of the domain
  // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
  const basename = process.env.BASENAME || "";

  return (
    <div>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          <Navbar />
          <Routes>
            <Route element={<Inicio />} path="/" />
            <Route element={<Acceso />} path="/acceso" />
            <Route element={<Demo />} path="/demo" />
            <Route element={<Alta_usuario />} path="/alta_usuario" />
            <Route element={<Password />} path="/password" />
            <Route element={<Single />} path="/single/:theid" />
            <Route element={<Perfil_Usuario />} path="/perfil_usuario" />
            <Route element={<Mis_reservas />} path="/mis_reservas" />
            <Route element={<h1> Not found! </h1>} />
          </Routes>{" "}
          <Footer />
        </ScrollToTop>{" "}
      </BrowserRouter>{" "}
    </div>
  );
};
export default injectContext(Layout);
