import React from "react";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";
import dynamic from "next/dynamic";

const ApiDocs = () => {
  return <SwaggerUI url="/api/swagger.json" />;
};

export default ApiDocs;