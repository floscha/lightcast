import argparse
import sys

from lightcast.core import search_podcasts


def run_wizard() -> None:
    print("Welcome to the LightCast wizard.")
    print("For more information, see https://github.com/floscha/lightcast\n")

    try:
        query = input("Podcast you want to download: ")
    except KeyboardInterrupt:
        sys.exit(0)

    search_results = search_podcasts(query)

    if not search_results:
        print("No podcasts could be found for your search...")
        sys.exit(0)

    for i, podcast in enumerate(search_results):
        print(f"{i+1}. {podcast.name}")

    podcast_index = int(input("\nEnter a number: "))
    selected_podcast = search_results[podcast_index - 1]
    print(f"You have selected {selected_podcast.name}")

    for i, episode in enumerate(selected_podcast.episodes):
        print(f"{i+1}. {episode.title}")

    episode_indices_input = input("\nWhich episode(s) to download? (comma-separated): ")
    episode_indices_tokens = [e.strip() for e in episode_indices_input.split(",")]
    episode_indices = [int(t) - 1 for t in episode_indices_tokens]

    for index in episode_indices:
        selected_podcast.episodes[index].download()


def search(args: list[str]) -> None:
    query = " ".join(args[1:])
    # Limit search results to 10 in order to reduce irrelevant results.
    # TODO: Make number of results configurable at some point.
    for i, podcast in enumerate(search_podcasts(query)[:10]):
        print(f"{i+1}. {podcast.name} (ID: {podcast.id})")


def list_episodes(args: list[str]) -> None:
    query = " ".join(args[1:])
    podcast = search_podcasts(query)[0]
    print(f"Episodes for {podcast.name!r}:")
    for i, episode in enumerate(podcast.episodes):
        print(f"\t{i+1}. {episode.title}")


def main():
    parser = argparse.ArgumentParser(description="A lightweight Python library for searching and downloading podcasts.")
    subparsers = parser.add_subparsers(dest="command", required=False)
    subparsers.add_parser("search", help="Search for something.")
    subparsers.add_parser("list-episodes", help="list available episodes.")
    
    args, unknown_args = parser.parse_known_args()

    match args.command:
        case None:
            run_wizard()
        case "search":
            search(unknown_args)
        case "list-episodes":
            list_episodes(unknown_args)
        case _:
            parser.print_help()
