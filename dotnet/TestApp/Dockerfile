# Example from https://dotnetplaybook.com/deploy-a-net-core-api-with-docker/
# Get Base Image (Full .NET Core SDK)
FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

# Copy everything else and build
COPY . ./
RUN dotnet restore .\\RestApi\\RestApi.csproj &&  dotnet publish -c Release -o .\\RestApi\\out .\\RestApi\\RestApi.csproj

# Generate runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
WORKDIR /app/RestApi
EXPOSE 5001
# Copy compiled dlls from sdk image to runtime image
COPY --from=build-env /app/RestApi/out .
ENTRYPOINT ["dotnet", "RestApi.dll"]