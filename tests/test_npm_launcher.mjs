import assert from "node:assert/strict";
import test from "node:test";
import { run } from "../bin/phoxia-devkit.mjs";

test("forwards init to the Python project command", () => {
  const calls = [];
  const status = run(["init", "--help"], {
    spawnSync(command, args) {
      calls.push([command, args]);
      return { status: 0 };
    },
  });
  assert.equal(status, 0);
  assert.deepEqual(calls[0][1].slice(-2), ["init", "--help"]);
});

test("returns 127 without Python", () => {
  assert.equal(run([], { spawnSync: () => ({ error: new Error("missing") }) }), 127);
});

test("rejects unsupported Node versions before spawning Python", () => {
  let called = false;
  assert.equal(run(["init"], { nodeVersion: "18.20.0", spawnSync: () => { called = true; } }), 1);
  assert.equal(called, false);
});
