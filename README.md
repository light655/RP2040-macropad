# RP2040-macropad
An 8 key macropad with multiple modes based on the RP2040 chip and circuitpython.

## English description
For English information about setting up the macro and string functions, please refer to [this repo](https://github.com/ooyang0325/8-key-macropad-no-light-pollution/).
This repo is a variation with the RGB LED on the Waveshare RP2040-Zero enabled.
The LED will flash the three colours in mode 3(printing a string), while it will flash green in mode 4(spamming a set of macro keys).

## 安裝步驟
1. 本專案使用CircuitPython開發，在安裝本軟體之前，需要先下載安裝[CircuitPython 7](https://circuitpython.org/board/raspberry_pi_pico/)。
2. 安裝CircuitPython時，先按著BOOT按鈕，再將USB線接上，會出現類似隨身碟的RPI-RP2裝置。將下載的CircuitPython UF2檔案複製貼上，等待RPI-RP2自動退出，即完成CircuitPython的安裝。
3. CircuitPython安裝完成後，會出現類似隨身碟的CIRCUITPY裝置，將本專案src資料夾的內容複製貼上，即完成軟體安裝

## 模式介紹
0. **停用按鍵**：當設定為模式0時，按下該按鍵將不會有任何反應。
1. **單點**：當設定為模式1時，按下該按鍵會輸出所設定的巨集鍵，然後隨即放開。
2. **連按**：當設定為模式2時，按下該按鍵會輸出所設定的巨集鍵，並且保持按著，直到放開該按鍵。
3. **字串**：當設定為模式3時，按下該按鍵會輸出所設定的字串。
4. **連點**：當設定為模式4時，按下該按鍵會迅速點擊所設定的巨集鍵，直到放開該按鍵。

## 設定步驟
1. 用Excel等試算表軟體打開**keys.csv**，如果是用LibreOffice的話，要把smart quote功能關掉。
2. 小鍵盤上的每一個按鍵會由CSV檔案中鉛直方向的兩格代表，上面的格子填入模式，下面的格子填入巨集鍵或字串。注意，第一行第二列在鍵盤上沒有按鍵，需要將模式設為0。
3. 設定**巨集**時，請使用不需要按Shift的按鍵，也就是說Shift需要分開寫。按鍵的名字可以參考**key_mapping.py**或是[這個網站](https://zhouer.org/KeyboardTest/)(記得把空格拿掉)。
