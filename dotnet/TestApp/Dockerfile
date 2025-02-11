# Example from https://dotnetplaybook.com/deploy-a-net-core-api-with-docker/
# Get Base Image (Full .NET Core SDK)
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build-env
WORKDIR /app

# Copy everything else and build
COPY . ./
RUN dotnet restore .\\RestApi\\RestApi.csproj &&  dotnet publish -c Release -o .\\RestApi\\out .\\RestApi\\RestApi.csproj

# Generate runtime image
FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /app/RestApi
# do i need 443?
EXPOSE 443 5001
# Copy compiled dlls from sdk image to runtime image
COPY --from=build-env /app/RestApi/out .
# Copy pfx cert for kestrel server
COPY --from=build-env /app/RestApi/aspnetapp.pfx .
ENTRYPOINT ["dotnet", "RestApi.dll"]