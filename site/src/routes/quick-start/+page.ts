import { redirect } from "@sveltejs/kit";

export function load() {
  redirect(308, "https://docs.phoxia.org/kit/quickstart");
}
