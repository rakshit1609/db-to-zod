import { z } from 'zod';

export const UsersSchema = z.object({
  id: z.number().int(),
  email: z.string(),
  full_name: z.string().nullable().optional(),
  created_at: z.string().datetime(),
});

export type Users = z.infer<typeof UsersSchema>;

export const SubscriptionsSchema = z.object({
  id: z.number().int(),
  user_id: z.number().int(),
  plan: z.string(),
  active: z.boolean(),
});

export type Subscriptions = z.infer<typeof SubscriptionsSchema>;
