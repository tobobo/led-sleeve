export class Router {
  constructor(location, config, container, routes) {
    for (let i = 0; i < routes.length; i++) {
      const MatchingRoute = routes[i](location, config, container);
      if (!!MatchingRoute) {
        this.route = new MatchingRoute(location, config, container);
        this.route.attach?.();
        break;
      }
    }
  }
}
