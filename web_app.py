import json
import urllib.error
import urllib.request

from flask import Flask, jsonify, render_template, request


IMAGE_MODEL = "gemini-2.5-flash-image"
TEXT_MODEL = "gemini-2.5-flash"

PRESETS = {
    "late-afternoon-luxury": {
        "title": "Modern Festive Facade",
        "note": "Warm light, wood accents, premium street view",
        "prompt": "modern luxury villa facade, late afternoon sun, balanced greenery, premium driveway, soft warm sky, elegant front elevation",
        "image": "/static/assets/late-afternoon-luxury.jpg",
        "position": "center 44%",
    },
    "modern-tropical": {
        "title": "Minimal Courtyard Home",
        "note": "Soft evening mood, clean landscape, calm facade",
        "prompt": "modern tropical house exterior, warm wood details, clean landscape, soft golden light, luxury residential presentation",
        "image": "/static/assets/modern-tropical.jpg",
        "position": "center 38%",
    },
    "minimal-gray": {
        "title": "Minimal Gray Villa",
        "note": "Luxury glazing, balanced garden, premium elevation",
        "prompt": "minimal gray luxury home, large windows, clean facade, calm landscape, elegant modern exterior, premium architecture",
        "image": "/static/assets/minimal-gray.jpg",
        "position": "center 46%",
    },
    "soft-morning": {
        "title": "Soft Morning Residence",
        "note": "Fresh landscape, bright facade, clean family home",
        "prompt": "clean luxury home exterior, soft morning light, fresh landscape, gentle blue sky, photo-real facade, refined residential style",
        "image": "/static/assets/soft-morning.jpg",
        "position": "center 42%",
    },
    "clean-courtyard": {
        "title": "Clean Courtyard Villa",
        "note": "Single-floor calm facade, wide yard, elegant entrance",
        "prompt": "single floor modern villa, spacious courtyard, balanced plants, elegant facade, realistic architectural photography, clean premium exterior",
        "image": "/static/assets/clean-courtyard.jpg",
        "position": "center 36%",
    },
    "tropical-night": {
        "title": "Tropical Night Home",
        "note": "Warm interior glow, lush garden, cozy evening mood",
        "prompt": "tropical evening house exterior, warm interior lighting, lush garden, elegant cozy facade, realistic night architectural visualization",
        "image": "/static/assets/tropical-night.jpg",
        "position": "center 34%",
    },
    "grand-glass-villa": {
        "title": "Grand Glass Villa",
        "note": "Three-story luxury home, glazing, premium frontage",
        "prompt": "three story luxury glass villa, premium landscape, large windows, warm interior lights, elegant residential elevation, photoreal exterior",
        "image": "/static/assets/grand-glass-villa.jpg",
        "position": "center 39%",
    },
    "slim-urban-house": {
        "title": "Slim Urban House",
        "note": "Vertical townhouse, planted balconies, clean modern lines",
        "prompt": "slim modern urban townhouse, planted balconies, minimalist facade, elegant city residence, realistic exterior visualization",
        "image": "/static/assets/slim-urban-house.jpg",
        "position": "center 32%",
    },
}


app = Flask(__name__)


def translate_api_error(message):
    lowered = message.lower()
    if "limit: 0" in lowered or "resource_exhausted" in lowered:
        return "Quota របស់ project នេះសម្រាប់ model នេះមិនអនុញ្ញាត free tier ទេ ឬបានអស់ហើយ។ សូមប្ដូរ model, ប្ដូរ project, ឬបើក billing។"
    if "exceeded your current quota" in lowered or "quota exceeded" in lowered:
        return "អ្នកបានអស់ quota សម្រាប់ project នេះហើយ។ សូមរង់ចាំ quota reset ឬបើក billing។"
    if "api key not valid" in lowered or "permission_denied" in lowered:
        return "API key មិនត្រឹមត្រូវ ឬ project/model នេះមិនមានសិទ្ធិចូលប្រើ។"
    if "model not found" in lowered or "not found" in lowered:
        return "Model name មិនត្រឹមត្រូវ ឬ model នេះមិនមានសម្រាប់ account/project របស់អ្នក។"
    return message


def post_gemini_request(model_name, api_key, payload):
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    request_obj = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request_obj, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(translate_api_error(f"Gemini API error {error.code}: {body}")) from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"បញ្ហា network ពេលហៅ Gemini API: {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Gemini API returned invalid JSON: {error}") from error


def extract_text(response_json):
    texts = []
    for candidate in response_json.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if part.get("text"):
                texts.append(part["text"].strip())
    return "\n".join(text for text in texts if text)


def extract_image_base64(response_json):
    for candidate in response_json.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and inline_data.get("data"):
                return inline_data["data"], inline_data.get("mimeType", "image/png")
    return None, None


def build_generation_prompt(data):
    preset_key = data.get("preset", "late-afternoon-luxury")
    preset = PRESETS.get(preset_key, PRESETS["late-afternoon-luxury"])
    prompt = data.get("prompt", "").strip()
    time_of_day = data.get("time_of_day", "Default")
    weather = data.get("weather", "Clear Skies")
    camera = data.get("camera", "Default")
    render_style = data.get("render_style", "Photo")
    parts = [
        preset["prompt"],
        prompt,
        f"Camera: {camera}.",
        f"Time of day: {time_of_day}.",
        f"Weather: {weather}.",
        f"Style target: {render_style}, realistic architectural visualization, high-end residential facade, photoreal result.",
    ]
    return " ".join(part for part in parts if part).strip()


@app.route("/")
def index():
    return render_template("index.html", presets=PRESETS, image_model=IMAGE_MODEL, text_model=TEXT_MODEL)


@app.post("/api/test-key")
def test_key():
    data = request.get_json(force=True)
    api_key = (data.get("apiKey") or "").strip()
    model_name = (data.get("modelName") or TEXT_MODEL).strip()
    if not api_key:
        return jsonify({"ok": False, "message": "សូមបញ្ចូល Gemini API key មុនពេល test។"}), 400

    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Reply with the exact text: API test successful."}]}],
        "generationConfig": {"responseModalities": ["TEXT"]},
    }
    try:
        response_json = post_gemini_request(model_name, api_key, payload)
    except RuntimeError as error:
        return jsonify({"ok": False, "message": str(error)}), 400

    return jsonify({"ok": True, "message": extract_text(response_json) or "API key test passed successfully."})


@app.post("/api/analyze")
def analyze():
    data = request.get_json(force=True)
    api_key = (data.get("apiKey") or "").strip()
    if not api_key:
        return jsonify({"ok": False, "message": "សូមបញ្ចូល Gemini API key មុនពេល analyze។"}), 400

    prompt = build_generation_prompt(data)
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{
                    "text": (
                        "You are an architectural visualization assistant. "
                        "Analyze this request and respond in 4 short lines: "
                        "1. facade style, 2. lighting advice, 3. landscaping advice, 4. render recommendation. "
                        f"User request: {prompt}"
                    )
                }],
            }
        ],
        "generationConfig": {"responseModalities": ["TEXT"]},
    }
    try:
        response_json = post_gemini_request(TEXT_MODEL, api_key, payload)
    except RuntimeError as error:
        return jsonify({"ok": False, "message": str(error)}), 400

    return jsonify({"ok": True, "message": extract_text(response_json) or "No analysis text returned."})


@app.post("/api/generate")
def generate():
    data = request.get_json(force=True)
    api_key = (data.get("apiKey") or "").strip()
    if not api_key:
        return jsonify({"ok": False, "message": "សូមបញ្ចូល Gemini API key មុនពេល generate។"}), 400

    prompt = build_generation_prompt(data)
    parts = [{"text": prompt}]

    image_data_url = data.get("imageDataUrl") or ""
    if image_data_url.startswith("data:") and "," in image_data_url:
        header, encoded = image_data_url.split(",", 1)
        mime_type = header.split(";")[0].replace("data:", "") or "image/jpeg"
        parts.append({"inlineData": {"mimeType": mime_type, "data": encoded}})

    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    try:
        response_json = post_gemini_request(IMAGE_MODEL, api_key, payload)
    except RuntimeError as error:
        return jsonify(
            {
                "ok": False,
                "message": str(error),
                "hint": "Text free tier អាចប្រើបានតាម gemini-2.5-flash ប៉ុន្តែ image model អាចត្រូវ billing ឬ image-model access។",
            }
        ), 400

    image_b64, mime_type = extract_image_base64(response_json)
    if not image_b64:
        return jsonify(
            {
                "ok": False,
                "message": "Gemini API did not return an image. Check the image model access and billing.",
            }
        ), 400

    return jsonify(
        {
            "ok": True,
            "imageDataUrl": f"data:{mime_type};base64,{image_b64}",
            "message": extract_text(response_json) or "Image generated successfully.",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
