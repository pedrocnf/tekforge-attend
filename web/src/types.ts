export type Role = 'ADMIN' | 'TEACHER' | 'STUDENT' | 'admin' | 'teacher' | 'student';

export interface User {
  id: string;
  username: string;
  full_name: string;
  email: string;
  role: Role;
  is_active: boolean;
  is_email_verified: boolean;
  created_at: string;
}

export interface Institution {
  id: string;
  name: string;
  cep: string;
  street: string;
  number: string;
  complement?: string | null;
  district: string;
  city: string;
  state: string;
  is_active: boolean;
  created_at: string;
}

export interface Discipline {
  id: string;
  name: string;
  institution_id: string;
  semester: string;
  academic_shift: string;
  period_label: string;
  weekly_meetings: { weekday: string; start_time: string; end_time: string }[];
  total_workload_hours: number;
  weekly_lessons_count: number;
  lesson_duration_minutes: number;
  is_active: boolean;
  created_at: string;
}

export interface Student {
  id: string;
  user_id: string;
  full_name: string;
  class_name: string;
  cpf: string;
  email: string;
  phone: string;
  created_at: string;
}

export interface Enrollment {
  id: string;
  student_user_id: string;
  discipline_id: string;
  is_active: boolean;
  created_at: string;
}

export interface AttendanceEvent {
  id: string;
  discipline_id: string;
  title: string;
  lesson_date: string;
  lesson_time: string;
  teacher_user_id: string;
  allow_remote_requests: boolean;
  status: string;
  created_at: string;
  closed_at?: string | null;
}

export interface AttendanceRequest {
  id: string;
  event_id: string;
  student_user_id: string;
  channel: string;
  stars?: number | null;
  tags: string[];
  comments?: string | null;
  status: string;
  requested_at: string;
  warning_distance?: boolean;
}
