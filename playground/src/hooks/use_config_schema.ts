const url = module
    ? `${athenaUrl}/modules/${module.type}/${module.name}/config_schema`
    : null;
  const { data, error, isLoading } = useSWR(url, athenaFetcher(athenaSecret));