import { redirect } from "@sveltejs/kit";

export function load() {
  redirect(308, "https://changelog.phoxia.org/kit");
}
