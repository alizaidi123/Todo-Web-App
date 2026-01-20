// Placeholder auth functions for compatibility
const auth = {};

export const signIn = () => Promise.resolve();
export const signUp = () => Promise.resolve();
export const signOut = () => Promise.resolve();

// Placeholder hook that returns null session
export const useSession = () => ({ session: null, isLoading: false });

export default auth;