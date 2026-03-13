import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 4000,      // จำนวน virtual users พร้อมกัน
  duration: '30s'  // ทดสอบ 30 วินาที
};

export default function () {
  http.get('https://kido-shusio.github.io/Choom-noom-Phrapathom/');
  sleep(1);  // หยุด 1 วินาที ก่อนส่ง request ถัดไป
}