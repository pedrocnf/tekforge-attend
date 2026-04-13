import { Card, CardContent, CardHeader } from '@mui/material';

export function SectionCard({
  title,
  action,
  children,
}: {
  title: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <Card>
      <CardHeader title={title} action={action} />
      <CardContent>{children}</CardContent>
    </Card>
  );
}
