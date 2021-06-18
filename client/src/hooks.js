import { handleSession } from 'svelte-kit-cookie-session';

/** @type {import('@sveltejs/kit').GetSession} */
export async function getSession({ locals }) {
  return locals.session.data;
}

export const handle = handleSession(
  {
    secret: import.meta.env.VITE_SECRET_KEY
  },
  ({ request, resolve }) => {
    // request.locals is populated with the session `request.locals.session`

    // Do anything you want here
    return resolve(request);
  }
);
