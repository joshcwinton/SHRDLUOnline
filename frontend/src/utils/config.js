export const getURI = () => {
  if(process.env.REACT_APP_PROD == "TRUE"){
    return "https://shrdluonline-backend.herokuapp.com";
  }
  else{
    return "http://127.0.0.1:5555";
  }
};
