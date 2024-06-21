import React, { useState, useEffect } from "react";
import axios, { AxiosResponse, AxiosError } from "axios";

interface Sensor {
  id: number;
  code: string;
}

function SensorList() {
  const [sensorList, setSensorList] = useState<Sensor[]>([]);

  useEffect(() => {
    axios.get<Sensor[]>('http://127.0.0.1:8000/api/v1/sensors/code')
      .then((response: AxiosResponse<Sensor[]>) => {
        console.log(response.data);
        setSensorList(response.data);
      })
      .catch((error: AxiosError) => {
        console.log(error);
      });
  }, []);

  const handleButtonClick = (code: string) => {
    console.log('Button clicked for sensor code:', code);
  };

  return (
    <div>
      <div>가상 센서 코드 목록</div>
      {sensorList.map(sensor => (
        <button key={sensor.code} onClick={() => handleButtonClick(sensor.code)}>
          {sensor.code}
        </button>
      ))}
    </div>
  );
}

export default SensorList;