<script>
    import { onMount } from 'svelte';
    let posts = [];

    async function fetchPosts() {
    const res = await fetch('http://localhost:8000/posts/');
    posts = await res.json();
    }

    onMount(fetchPosts);
</script>

<div>
    {#each posts as post (post.id)}
    <h2>{post.title}</h2>
    <p>{post.content}</p>
    {/each}
</div>
