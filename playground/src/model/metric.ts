type Metric = {
    title: string;
    summary: string;
    description: MetricDescription;
}

type MetricDescription = {
    good: string;
    mid: string;
    bad: string;
}