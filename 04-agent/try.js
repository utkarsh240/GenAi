const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, ".env") });




const { OpenAI } = require("openai");
const axios = require("axios");
const readline = require("readline-sync");
const { execSync } = require("child_process");


const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function getWeather(city) {
  try {
    const url = `https://wttr.in/${city}?format=%C+%t`;
    const response = await axios.get(url);
    return `The weather in ${city} is ${response.data}.`;
  } catch (error) {
    return "Something went wrong";
  }
}

function runCommand(cmd) {
  try {
    return execSync(cmd, { encoding: "utf8" });
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

const availableTools = {
  get_weather: getWeather,
  run_command: runCommand
};

const SYSTEM_PROMPT = `
You are a helpful AI Assistant specialized in resolving user queries.
You work in start, plan, action, observe mode.

For the given user query and available tools, plan the step-by-step execution.
Based on the planning, select the relevant tool from the available tools and call it.

Wait for the observation and, based on that, resolve the user query.

Rules:
- Follow the Output JSON Format.
- Always perform one step at a time and wait for next input.
- Carefully analyze the user query.

Output JSON Format:
{
  "step": "string",
  "content": "string",
  "function": "The name of function if the step is action",
  "input": "The input parameter for the function"
}

Available Tools:
- "get_weather": Takes a city name as input and returns current weather.
- "run_command": Takes a Linux command as string and returns output after execution.
`;

let messages = [
  { role: "system", content: SYSTEM_PROMPT }
];

(async function main() {
  while (true) {
    const query = readline.question("> ");
    messages.push({ role: "user", content: query });

    while (true) {
      const chatResponse = await openai.chat.completions.create({
        model: "gpt-4.1",
        response_format: { type: "json_object" },
        messages
      });

      const assistantMessage = chatResponse.choices[0].message.content;
      messages.push({ role: "assistant", content: assistantMessage });

      const parsed = JSON.parse(assistantMessage);

      if (parsed.step === "plan") {
        console.log("🧠:", parsed.content);
        continue;
      }

      if (parsed.step === "action") {
        const tool = parsed.function;
        const input = parsed.input;
        console.log(`🛠️: Calling tool: ${tool} with input: ${input}`);

        if (availableTools[tool]) {
          const output = await availableTools[tool](input);
          messages.push({
            role: "user",
            content: JSON.stringify({ step: "observe", output })
          });
          continue;
        }
      }

      if (parsed.step === "output") {
        console.log("🤖:", parsed.content);
        break;
      }
    }
  }
})();
