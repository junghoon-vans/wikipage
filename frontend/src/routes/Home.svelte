<script>
    import { onMount } from "svelte";
    import { PUBLIC_BASE_URL } from '$env/static/public';
    import axios from "axios";

    let posts = [];

    const client = axios.create({
        baseURL: PUBLIC_BASE_URL,
        headers: {
            'Content-Type': 'application/json',
        },
    })

    onMount(async () => {
        try {
            const res = await client.get("/posts");
            posts = res.data;
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });
</script>

<div class="flex flex-col">
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
            <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                {#if posts.length > 0}
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created At</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            {#each posts as post}
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-gray-900">
                                            {post.title}
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-gray-500">
                                            {new Date(post.created_at / 1000).toLocaleString()}
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {:else}
                    <div class="text-center text-gray-500">No posts found.</div>
                {/if}
            </div>
        </div>
    </div>
</div>
