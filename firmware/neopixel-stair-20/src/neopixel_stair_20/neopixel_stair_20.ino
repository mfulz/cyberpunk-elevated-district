#include <Adafruit_NeoPixel.h>

// WeAct BlackPill STM32F401CCU6 / STM32duino 2.9.0
constexpr uint32_t DATA_PIN = PA8;
constexpr uint16_t PIXEL_COUNT = 20;

// Einzelpixel-Helligkeiten: Die letzte LED der Kette sitzt ohne Spacer direkt
// unter dem Diffusor und bleibt deshalb auf der bisherigen Helligkeit.
constexpr uint8_t NORMAL_BRIGHTNESS = 255; // 100 %
constexpr uint8_t LAST_BRIGHTNESS = 128;   // ca. 50 %

Adafruit_NeoPixel pixels(PIXEL_COUNT, DATA_PIN, NEO_GRB + NEO_KHZ800);

// Die Kette verlaeuft physisch von oben nach unten:
// Pixel 0 = oberste Stufe, Pixel PIXEL_COUNT - 1 = unterste Stufe.
uint16_t pixelForStep(uint16_t stepFromBottom) {
  return PIXEL_COUNT - 1 - stepFromBottom;
}

constexpr uint16_t THEME_A_BASE_HUE = 50000;   // Kraeftiges Lila
constexpr uint16_t THEME_A_RUNNER_HUE = 62000; // Warmes Neonrot/Pink
constexpr uint16_t THEME_B_BASE_HUE = 43690;   // Blau
constexpr uint16_t THEME_B_RUNNER_HUE = 32768; // Cyan
constexpr uint16_t THEME_C_BASE_HUE = 65000;   // Tiefes Crimson
constexpr uint16_t THEME_C_RUNNER_HUE = 7000;  // Amber/Gold

int32_t shortestHueDelta(uint16_t from, uint16_t to) {
  int32_t delta = static_cast<int32_t>(to) - from;
  if (delta > 32767) {
    delta -= 65536;
  } else if (delta < -32768) {
    delta += 65536;
  }
  return delta;
}

uint16_t interpolateHueByDelta(uint16_t from, int32_t delta, uint8_t amount) {
  return static_cast<uint16_t>(
      static_cast<int32_t>(from) + delta * amount / 255);
}

uint16_t interpolateHueShortest(uint16_t from, uint16_t to, uint8_t amount) {
  return interpolateHueByDelta(from, shortestHueDelta(from, to), amount);
}

uint32_t blendedColor(uint16_t baseHue, uint16_t runnerHue,
                      uint8_t runnerStrength, uint8_t brightness) {
  // Auch innerhalb eines Schemas im HSV-Farbraum ueberblenden. So bleiben
  // die Farben satt und erzeugen keine schmutzigen RGB-Mischfarben.
  const uint16_t hue =
      interpolateHueShortest(baseHue, runnerHue, runnerStrength);
  return pixels.ColorHSV(hue, 255, brightness);
}

void setup() {
  pixels.begin();
  pixels.setBrightness(255); // Helligkeit wird gezielt pro Pixel gesetzt.
  pixels.clear();
  pixels.show();
}

void loop() {
  // Q8-Position: 256 Einheiten entsprechen exakt einer Stufe. Der Runner ist
  // 3 Stufen breit. Seine Intensitaet pro LED ergibt sich aus der
  // Ueberdeckung mit der jeweiligen Stufe; dadurch faden die Randstufen weich,
  // waehrend die effektive Gesamtbreite exakt 3 Stufen bleibt.
  static uint16_t runnerPosition = 0;
  static uint8_t themeCycle = 0;
  constexpr uint16_t UNITS_PER_STEP = 256;
  constexpr uint16_t RUNNER_WIDTH = 3 * UNITS_PER_STEP;
  constexpr uint16_t RUNNER_HALF_WIDTH = RUNNER_WIDTH / 2;
  constexpr int32_t RUNNER_START =
      -static_cast<int32_t>(RUNNER_HALF_WIDTH) - UNITS_PER_STEP / 2;
  constexpr uint16_t TRAVEL_LENGTH =
      PIXEL_COUNT * UNITS_PER_STEP + RUNNER_WIDTH;
  const int32_t runnerQ8 = RUNNER_START + runnerPosition;

  // 12 Laeufe bilden einen vollstaendigen Themenzyklus. Jedes Schema bleibt
  // drei Laeufe stabil. Im jeweils vierten Lauf traegt der Runner das neue
  // Schema von unten nach oben: Vor ihm bleibt die alte Grundfarbe erhalten,
  // hinter ihm bleibt die neue Grundfarbe stehen.
  bool wipeActive = false;
  uint16_t baseHueFrom;
  uint16_t baseHueTo;
  uint16_t runnerHue;
  if (themeCycle < 3) {
    baseHueFrom = THEME_A_BASE_HUE;
    baseHueTo = THEME_A_BASE_HUE;
    runnerHue = THEME_A_RUNNER_HUE;
  } else if (themeCycle == 3) {
    wipeActive = true;
    baseHueFrom = THEME_A_BASE_HUE;
    baseHueTo = THEME_B_BASE_HUE;
    runnerHue = THEME_B_RUNNER_HUE;
  } else if (themeCycle < 7) {
    baseHueFrom = THEME_B_BASE_HUE;
    baseHueTo = THEME_B_BASE_HUE;
    runnerHue = THEME_B_RUNNER_HUE;
  } else if (themeCycle == 7) {
    wipeActive = true;
    baseHueFrom = THEME_B_BASE_HUE;
    baseHueTo = THEME_C_BASE_HUE;
    runnerHue = THEME_C_RUNNER_HUE;
  } else if (themeCycle < 11) {
    baseHueFrom = THEME_C_BASE_HUE;
    baseHueTo = THEME_C_BASE_HUE;
    runnerHue = THEME_C_RUNNER_HUE;
  } else {
    wipeActive = true;
    baseHueFrom = THEME_C_BASE_HUE;
    baseHueTo = THEME_A_BASE_HUE;
    runnerHue = THEME_A_RUNNER_HUE;
  }

  // Alle Stufen tragen dauerhaft die aktuelle Grundfarbe. Der 3 Stufen
  // breite Akzent wandert hoch und fadet an seinen beiden Kanten weich.
  for (uint16_t step = 0; step < PIXEL_COUNT; ++step) {
    const int32_t stepQ8 = static_cast<int32_t>(step) * UNITS_PER_STEP;
    const int32_t runnerLeft = runnerQ8 - RUNNER_HALF_WIDTH;
    const int32_t runnerRight = runnerQ8 + RUNNER_HALF_WIDTH;
    const int32_t stepLeft = stepQ8 - UNITS_PER_STEP / 2;
    const int32_t stepRight = stepQ8 + UNITS_PER_STEP / 2;
    const int32_t overlapLeft = runnerLeft > stepLeft ? runnerLeft : stepLeft;
    const int32_t overlapRight = runnerRight < stepRight ? runnerRight : stepRight;
    const int32_t overlap = overlapRight > overlapLeft
                                ? overlapRight - overlapLeft
                                : 0;
    const uint8_t strength = static_cast<uint8_t>(
        overlap >= UNITS_PER_STEP ? 255 : overlap * 255 / UNITS_PER_STEP);

    uint8_t wipeAmount = 0;
    if (wipeActive) {
      const int32_t passedDistance = runnerQ8 - stepQ8;
      if (passedDistance >= static_cast<int32_t>(RUNNER_HALF_WIDTH)) {
        wipeAmount = 255;
      } else if (passedDistance > -static_cast<int32_t>(RUNNER_HALF_WIDTH)) {
        wipeAmount = static_cast<uint8_t>(
            (passedDistance + RUNNER_HALF_WIDTH) * 255 / RUNNER_WIDTH);
      }
    }
    const uint16_t baseHue = interpolateHueShortest(
        baseHueFrom, baseHueTo, wipeAmount);

    const uint16_t physicalPixel = pixelForStep(step);
    const uint8_t brightness =
        physicalPixel == PIXEL_COUNT - 1 ? LAST_BRIGHTNESS : NORMAL_BRIGHTNESS;
    pixels.setPixelColor(
        physicalPixel, blendedColor(baseHue, runnerHue, strength, brightness));
  }

  pixels.show();
  runnerPosition += 6;
  if (runnerPosition >= TRAVEL_LENGTH) {
    runnerPosition -= TRAVEL_LENGTH;
    themeCycle = (themeCycle + 1) % 12;
  }
  delay(28);  // Knapp 1,2 Sekunden pro Stufe; Laufgeschwindigkeit bleibt konstant.
}
