import { request } from '../utils/request';
import { SportTag, UserProfile } from './user';

export interface Activity {
  id: number;
  title: string;
  description: string;
  sport_tag: SportTag;
  start_time: string;
  end_time?: string;
  latitude: number;
  longitude: number;
  address: string;
  max_participants: number;
  current_participants: number;
  gender_requirement: number;
  registration_deadline: string;
  status: number;
  cover_url: string;
  creator: Pick<UserProfile, 'id' | 'nickname' | 'avatar_url' | 'gender' | 'bio' | 'sport_tags'>;
  distance_meters?: number;
  is_joined: boolean;
  created_at: string;
}

export interface ActivityDetail extends Activity {
  participants: Array<{
    user: Activity['creator'];
    joined_at: string;
  }>;
}

export interface ActivityCreatePayload {
  title: string;
  description?: string;
  sport_tag_id: number;
  start_time: string;
  end_time?: string;
  latitude: number;
  longitude: number;
  address?: string;
  max_participants: number;
  gender_requirement?: number;
  registration_deadline: string;
}

export function listActivities(params?: {
  lat?: number;
  lng?: number;
  radius?: number;
  sport_tag_id?: number;
}): Promise<Activity[]> {
  return request<Activity[]>({ url: '/activities', data: params });
}

export function getActivity(id: number, params?: { lat?: number; lng?: number }): Promise<ActivityDetail> {
  return request<ActivityDetail>({ url: `/activities/${id}`, data: params });
}

export function createActivity(data: ActivityCreatePayload): Promise<ActivityDetail> {
  return request<ActivityDetail>({ url: '/activities', method: 'POST', data });
}

export function joinActivity(id: number): Promise<ActivityDetail> {
  return request<ActivityDetail>({ url: `/activities/${id}/join`, method: 'POST' });
}

export function cancelJoin(id: number): Promise<ActivityDetail> {
  return request<ActivityDetail>({ url: `/activities/${id}/join`, method: 'DELETE' });
}

export function cancelActivity(id: number): Promise<ActivityDetail> {
  return request<ActivityDetail>({ url: `/activities/${id}/cancel`, method: 'PUT' });
}

export function listMyCreated(): Promise<Activity[]> {
  return request<Activity[]>({ url: '/activities/my/created' });
}

export function listMyJoined(): Promise<Activity[]> {
  return request<Activity[]>({ url: '/activities/my/joined' });
}
