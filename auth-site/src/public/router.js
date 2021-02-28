export class Router {
  constructor(location, config, routes) {
    for (let i = 0; i < routes.length; i++) {
      const MatchingRoute = routes[i](location, config);
      if (!!MatchingRoute) {
        this.route = new MatchingRoute(location, config);
        this.route.attach?.();
        break;
      }
    }
  }
}
