export class Router {
  constructor(location, routes) {
    for (let i = 0; i < routes.length; i++) {
      const MatchingRoute = routes[i](location);
      if (!!MatchingRoute) {
        this.route = new MatchingRoute(location);
        this.route.attach?.();
        break;
      }
    }
  }
}
