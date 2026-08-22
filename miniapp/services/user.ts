import { request } from '../utils/request';

export interface SportTag {
  id: number;
  name: string;
  icon: string;
  sort_order: number;
}

export interface UserProfile {
  id: number;
  nickname: string;
  avatar_url: string;
  gender: number;
  bio: string;
  latitude?: number;
  longitude?: number;
  location_updated_at?: string;
  sport_tags: SportTag[];
  created_at: string;
}

export interface UserUpdatePayload {
  nickname?: string;
  avatar_url?: string;
  gender?: number;
  bio?: string;
  sport_tag_ids?: number[];
}

export function getMe(): Promise<UserProfile> {
  return request<UserProfile>({ url: '/users/me' });
}

export function updateMe(data: UserUpdatePayload): Promise<UserProfile> {
  return request<UserProfile>({ url: '/users/me', method: 'PUT', data });
}

export function updateLocation(latitude: number, longitude: number): Promise<UserProfile> {
  return request<UserProfile>({
    url: '/users/location',
    method: 'POST',
    data: { latitude, longitude },
  });
}

export function getSportTags(): Promise<SportTag[]> {
  return request<SportTag[]>({ url: '/sport-tags', auth: false });
}
