export function formatDateTime(iso: string): string {
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getMonth() + 1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function statusText(status: number): string {
  const map: Record<number, string> = {
    1: '招募中',
    2: '已满员',
    3: '进行中',
    4: '已结束',
    5: '已取消',
  };
  return map[status] || '未知';
}

export function genderRequirementText(value: number): string {
  const map: Record<number, string> = { 0: '不限', 1: '仅男', 2: '仅女' };
  return map[value] || '不限';
}
