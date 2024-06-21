import React from "react";
import { createRoot } from 'react-dom/client';
import SensorList from "./sensor";

const rootElement = document.getElementById('root');

if (rootElement) {
  const root = createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <SensorList />
    </React.StrictMode>
  );
}