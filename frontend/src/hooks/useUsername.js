import { useAuth } from "react-oidc-context";

export const useUsername = () => {
  const auth = useAuth();
  
  if (!auth.isAuthenticated || !auth.user) {
    return null;
  }

  const profile = auth.user.profile;
  // Try email first, then cognito:username, then preferred_username
  return profile?.email || profile?.['cognito:username'] || profile?.preferred_username || null;
};
