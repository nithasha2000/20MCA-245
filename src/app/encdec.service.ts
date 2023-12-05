import { Injectable } from '@angular/core';
import * as CryptoJS from 'crypto-js';

@Injectable({
  providedIn: 'root'
})
export class EncDecService {
  constructor() {}

  set(keys: any, value: any) {
    const key = CryptoJS.enc.Utf8.parse(keys);
    let iv = CryptoJS.lib.WordArray.random(16); // Generate a random IV

    // Ensure IV is 16 bytes by appending zero bytes if needed
    while (iv.words.length < 4) {
      iv.words.push(0);
    }

    const encrypted = CryptoJS.AES.encrypt(
      CryptoJS.enc.Utf8.parse(value.toString()),
      key,
      {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
      }
    );

    // Concatenate IV and encrypted data for transmission
    const combined = CryptoJS.lib.WordArray.create();
    combined.concat(iv);
    combined.concat(encrypted.ciphertext);

    return combined.toString(CryptoJS.enc.Base64);
  }
}
