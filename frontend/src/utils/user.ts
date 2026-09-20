import { User } from '../types';

/**
 * Derives the dynamic display name for an authenticated or guest user.
 * Strictly adheres to the fallback hierarchy:
 *   1. display_name
 *   2. first_name + last_name
 *   3. first_name
 *   4. username
 *   5. "User"
 *
 * Never falls back to a hardcoded personal name.
 */
export function getUserDisplayName(user: User | null | undefined): string {
  if (!user) {
    return 'User';
  }

  if (user.display_name && user.display_name.trim()) {
    return user.display_name.trim();
  }

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(' ').trim();
  if (fullName) {
    return fullName;
  }

  if (user.first_name && user.first_name.trim()) {
    return user.first_name.trim();
  }

  if (user.username && user.username.trim()) {
    return user.username.trim();
  }

  return 'User';
}

/**
 * Returns the first letter of the user's display name for avatars.
 * Defaults to 'U' if not available.
 */
export function getUserInitial(user: User | null | undefined): string {
  const name = getUserDisplayName(user);
  return (name[0] || 'U').toUpperCase();
}

/**
 * Safely returns the user's email address or an empty string.
 */
export function getUserEmail(user: User | null | undefined): string {
  return user?.email || '';
}
